class DBPropertyUtil:
    @staticmethod
    def get_connection_string(prop_file_name: str) -> str:
        props = {}
        try:
            with open(prop_file_name, 'r') as file:
                for line in file:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key_value = line.split('=')
                        if len(key_value) == 2:
                            key, value = key_value
                            props[key.strip()] = value.strip()
        except FileNotFoundError:
            print(f"Property file '{prop_file_name}' not found.")
        except Exception as e:
            print(f"Error reading property file: {e}")

        # Build connection string from properties
        connection_string = (
            f"host={props.get('host')};"
            f"user={props.get('user')};"
            f"password={props.get('password')};"
            f"database={props.get('database')}"
        )
        return connection_string
