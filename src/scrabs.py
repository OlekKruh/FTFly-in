def dispatch(self, line_list: List):
    if line_list[0] == "nb_drones":
        try:
            if len(line_list[1]) != 1:
                error_exit(f"Error: 'nb_drones' expects 1 value, "
                           f"got {len(line_list[1])}")
            self.world.drones_quantity = int(line_list[1][0])
        except (ValueError, IndexError, TypeError) as e:
            error_exit(f"Error nb_drones: {e}")

    elif line_list[0] in ["start_hub", "hub", "end_hub"]:
        try:
            main_param = line_list[1]
            meta_data = line_list[2] if len(line_list) > 2 else None
            if len(main_param) != 3:
                error_exit(f"Error: {line_list[0]} expects [name, x, y],"
                           f" got {main_param}")
            hub_name, hub_x, hub_y = (
                line_list[1][0],
                int(line_list[1][1]),
                int(line_list[1][2])
            )
            self.world.add_zone_to_map(
                [hub_name, hub_x, hub_y],
                meta_data  # выпадаем за список нужно условие
            )
        except (ValueError, IndexError) as e:
            error_exit(f"Error hub: Invalid main parameters format "
                       f"or missing values. {e}")

    elif line_list[0] == "connection":
        try:
            connection = line_list[1]
            meta_data = line_list[2] if len(line_list) > 2 else None
            if len(connection) != 1:
                error_exit("Invalid value. "
                           "Onli one connection must be in line "
                           f"got {connection}")
            self.world.add_relation_to_map(connection[0], meta_data[0])
        except (ValueError, IndexError) as e:
            error_exit(f"Error: Invalid connection parameters format "
                       f"or missing values. {e}")