import numpy


class MinimumCurvaturePath:
    def __init__(self, startpoint: tuple[float, ...], endpoint: tuple[float, ...], resolution: int = 1000, \
                 random_walk_radius_range: tuple[float, float] = (0.3, 0.6), random_walk_points: int = 50) -> None:
        self.startpoint = startpoint
        self.endpoint = endpoint
        self.resolution = resolution
        self.dx = self.endpoint[0] - self.startpoint[0]
        self.dy = self.endpoint[1] - self.startpoint[1]
        self.dz = self.endpoint[2] - self.startpoint[2]
        # circle_radius = 0.5 * numpy.sqrt((self.dx**2 + self.dy**2 + self.dz**2)*(1+self.dz**2/(self.dx**2 + self.dy**2)))
        circle_radius = 0.5 * (self.dx ** 2 + self.dy ** 2 + self.dz ** 2) / numpy.sqrt(self.dx ** 2 + self.dy ** 2)
        azimuth_angle = numpy.arctan2(self.dy, self.dx)
        circle_x = circle_radius * numpy.cos(azimuth_angle)
        circle_y = circle_radius * numpy.sin(azimuth_angle)
        center = (circle_x + self.startpoint[0], circle_y + self.startpoint[1], self.startpoint[2])
        t_values = numpy.linspace(0, 1, self.resolution)
        phi_max = numpy.arctan(
            numpy.abs(self.dz) / numpy.sqrt((center[0] - self.endpoint[0]) ** 2 + (center[1] - self.endpoint[1]) ** 2))
        phi = phi_max * t_values

        self.par_x = center[0] - circle_radius * numpy.cos(azimuth_angle) * numpy.cos(phi)
        self.par_y = center[1] - circle_radius * numpy.sin(azimuth_angle) * numpy.cos(phi)
        self.par_z = center[2] - circle_radius * numpy.sin(phi)

        random_walk_x, random_walk_y = RandomWalk(self.resolution, random_walk_radius_range, random_walk_points).arrays
        self.par_x += random_walk_x
        self.par_y += random_walk_y

        self.index = 0

    def __str__(self):
        return f"x = {self.par_x}\n\ny = {self.par_y}\n\nz = {self.par_z}"

    def get_next_point(self) -> tuple[float, ...]:
        point = (self.par_x[self.index], self.par_y[self.index], self.par_z[self.index])
        self.index += 1
        self.index %= self.resolution
        return point


class RandomWalk:
    def __init__(self, resolution: int, radius_range: tuple[float, float], num_of_points: int) -> None:
        self.resolution = resolution
        self.radius_range = radius_range
        self.num_of_points = num_of_points
        self.arrays = self.generate_arrays()

    def generate_arrays(self) -> tuple[numpy.ndarray, numpy.ndarray]:
        radii = numpy.random.uniform(*self.radius_range, self.num_of_points - 2)
        thetas = numpy.random.uniform(0, 2 * numpy.pi, self.num_of_points - 2)

        x_points = numpy.r_[0, radii * numpy.cos(thetas), 0]
        y_points = numpy.r_[0, radii * numpy.sin(thetas), 0]

        x_interpolated = numpy.interp(numpy.linspace(1, self.num_of_points, self.resolution),
                                      numpy.linspace(1, self.num_of_points, self.num_of_points), x_points)
        y_interpolated = numpy.interp(numpy.linspace(1, self.num_of_points, self.resolution),
                                      numpy.linspace(1, self.num_of_points, self.num_of_points), y_points)

        return x_interpolated, y_interpolated


class SafetyMarginSurface:
    def __init__(self, mcp: MinimumCurvaturePath, margin=1, resolution=50) -> None:
        THETA_RESOLUTION = 24

        # todo: px og px_s1 bør byttes om på.
        px = mcp.par_x[1:]
        length, = px.shape
        py = mcp.par_y[1:]
        pz = mcp.par_z[1:]
        # shift all values one in order to calculate the tangential vectors.
        px_s1 = mcp.par_x[:-1]
        py_s1 = mcp.par_y[:-1]
        pz_s1 = mcp.par_z[:-1]

        # todo: disse bør flippes!
        dx = px - px_s1
        dy = py - py_s1
        dz = pz - pz_s1
        dxy = numpy.sqrt(dx ** 2 + dy ** 2)
        tang_len = numpy.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

        # calculate vectors perpendicular to tangent vectors.
        perp_x = -dx * dz / dxy
        perp_y = -dy * dz / dxy
        perp_z = dxy
        perp_len = numpy.sqrt(perp_x ** 2 + perp_y ** 2 + perp_z ** 2)

        # normalize
        perp_x /= perp_len
        perp_y /= perp_len
        perp_z /= perp_len
        tang_x = dx / tang_len
        tang_y = dy / tang_len
        tang_z = dz / tang_len

        # matrices with points that will be returned.
        x_mat = numpy.zeros((THETA_RESOLUTION, resolution))
        y_mat = numpy.zeros((THETA_RESOLUTION, resolution))
        z_mat = numpy.zeros((THETA_RESOLUTION, resolution))

        for k, theta in enumerate(numpy.linspace(-numpy.pi / 2, 3 * numpy.pi / 2, THETA_RESOLUTION)):

            rot_x = []
            rot_y = []
            rot_z = []

            # todo: run interpolation earlier, so that this loop can be run 'resolution' number of times
            for i in range(length):
                n1, n2, n3 = tang_x[i], tang_y[i], tang_z[i]
                p1, p2, p3 = perp_x[i], perp_y[i], perp_z[i]
                rot_matrix = numpy.array((
                    (numpy.cos(theta) + n1 ** 2 * (1 - numpy.cos(theta)),
                     n1 * n2 * (1 - numpy.cos(theta)) - n3 * numpy.sin(theta),
                     n1 * n2 * (1 - numpy.cos(theta)) + n2 * numpy.sin(theta)),
                    (n1 * n2 * (1 - numpy.cos(theta)) + n3 * numpy.sin(theta),
                     numpy.cos(theta) + n2 ** 2 * (1 - numpy.cos(theta)),
                     n2 * n3 * (1 - numpy.cos(theta)) - n1 * numpy.sin(theta)),
                    (n1 * n3 * (1 - numpy.cos(theta)) - n2 * numpy.sin(theta),
                     n2 * n3 * (1 - numpy.cos(theta)) + n1 * numpy.sin(theta),
                     numpy.cos(theta) + n3 ** 2 * (1 - numpy.cos(theta))),
                ))
                r1, r2, r3 = rot_matrix.dot(numpy.array((p1, p2, p3)))

                rot_x.append(r1)
                rot_y.append(r2)
                rot_z.append(r3)

            rot_x = numpy.array(rot_x)
            rot_y = numpy.array(rot_y)
            rot_z = numpy.array(rot_z)
            rot_len = numpy.sqrt(rot_x ** 2 + rot_y ** 2 + rot_z ** 2)

            rot_x *= margin / rot_len
            rot_y *= margin / rot_len
            rot_z *= margin / rot_len

            point_x = numpy.interp(numpy.linspace(1, length, resolution), numpy.linspace(1, length, length), rot_x + px)
            point_y = numpy.interp(numpy.linspace(1, length, resolution), numpy.linspace(1, length, length), rot_y + py)
            point_z = numpy.interp(numpy.linspace(1, length, resolution), numpy.linspace(1, length, length), rot_z + pz)

            for j in range(resolution):
                x_mat[k, j] = point_x[j]
                y_mat[k, j] = point_y[j]
                z_mat[k, j] = point_z[j]

        self.to_plot = x_mat, y_mat, z_mat
