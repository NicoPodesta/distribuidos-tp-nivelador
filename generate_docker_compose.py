import sys

OUTPUT_FILE = "docker-compose.yaml"
SERVER_NAME = "server"
SERVER_BUILD_CONTEXT = "./services/server"
CLIENT_BUILD_CONTEXT = "./services/client"
DOCKERFILE = "Dockerfile"
SERVER_PORT = 5678
VOLUME_INPUT = "./input:/input:ro"
VOLUME_OUTPUT = "./output:/output:rw"
INPUT_FILE_TEMPLATE = "/input/input-{id}.csv"
OUTPUT_FILE_TEMPLATE = "/output/output-{id}.csv"


def write_server_service(file) -> None:
    file.write("services:\n")
    file.write(f"  {SERVER_NAME}:\n")
    file.write("    build:\n")
    file.write(f"      context: {SERVER_BUILD_CONTEXT}\n")
    file.write(f"      dockerfile: {DOCKERFILE}\n")
    file.write(f"    container_name: {SERVER_NAME}\n")
    file.write("    ports:\n")
    file.write(f'      - "{SERVER_PORT}:{SERVER_PORT}"\n')
    file.write("    environment:\n")
    file.write("      - PYTHONUNBUFFERED=1\n")
    file.write(f"      - SERVER_HOST={SERVER_NAME}\n")
    file.write(f"      - SERVER_PORT={SERVER_PORT}\n")


def write_client_service(file, agency_id: int) -> None:
    client_name = f"client_{agency_id}"
    input_path = INPUT_FILE_TEMPLATE.format(id=agency_id)
    output_path = OUTPUT_FILE_TEMPLATE.format(id=agency_id)

    file.write(f"  {client_name}:\n")
    file.write("    build:\n")
    file.write(f"      context: {CLIENT_BUILD_CONTEXT}\n")
    file.write(f"      dockerfile: {DOCKERFILE}\n")
    file.write(f"    container_name: {client_name}\n")
    file.write("    depends_on:\n")
    file.write(f"      - {SERVER_NAME}\n")
    file.write("    volumes:\n")
    file.write(f"      - {VOLUME_INPUT}\n")
    file.write(f"      - {VOLUME_OUTPUT}\n")
    file.write("    environment:\n")
    file.write(f"      - AGENCY_ID={agency_id}\n")
    file.write(f"      - SERVER_HOST={SERVER_NAME}\n")
    file.write(f"      - SERVER_PORT={SERVER_PORT}\n")
    file.write(f"      - INPUT_FILE={input_path}\n")
    file.write(f"      - OUTPUT_FILE={output_path}\n")


def generate_file(num_clients: int, file_path: str) -> None:
    with open(file_path, "w", encoding="utf-8") as file:
        write_server_service(file)
        for client_id in range(num_clients):
            file.write("\n")
            write_client_service(file, client_id)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 generate_docker_compose.py <num_clients>", file=sys.stderr)
        return

    try:
        num_clients = int(sys.argv[1])
        if num_clients <= 0:
            raise ValueError("The number of clients must be a positive integer greater than zero.")
    except ValueError as err:
        print(f"Parameter error:: {err}", file=sys.stderr)
        return

    try:
        generate_file(num_clients, OUTPUT_FILE)
        print(f"{OUTPUT_FILE} successfully generated with {num_clients} clients.")
    except OSError as err:
        print(f"Write error: {err}", file=sys.stderr)


if __name__ == "__main__":
    main()
