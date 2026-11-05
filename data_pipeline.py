from typing import Protocol
from data_stream import DataStream as BaseDataStream


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CsvExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = [val for rank, val in data]
        print(f"CSV output: \n{",".join(values)}")


class JsonExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        json_parts = []
        for rank, val in data:
            json_parts.append(f'"item_{rank}": "{val}"')

        json_str = "{" + ",".join(json_parts) + "}"
        print(f"JSON output: \n{json_str}")


class DataStream(BaseDataStream):
    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            exported_data: list[tuple[int, str]] = []

            for _ in range(nb):
                if proc.remaining_count > 0:
                    rank, val = proc.output()
                    exported_data.append((rank, val))

            if exported_data:
                plugin.process_output(exported_data)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Initialize Data Stream...\n")
    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Processors\n")
    from data_processor import NumericProcessor, TextProcessor, LogProcessor
    num_proc = NumericProcessor()
    txt_proc = TextProcessor()
    log_proc = LogProcessor()

    stream.register_processor(num_proc)
    stream.register_processor(txt_proc)
    stream.register_processor(log_proc)

    batch1 = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead"
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected"
            }
        ],
        42,
        ["Hi", "five"]
    ]

    print(f"Send first batch of data on stream: {batch1}\n")
    stream.process_stream(batch1)
    stream.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:\n")
    csv_plugin = CsvExportPlugin()
    stream.output_pipeline(3, csv_plugin)

    stream.print_processors_stats()

    # Segundo lote e teste do JSON plugin
    batch2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR",
             "log_message": "500 server crash"
             },
            {"log_level": "NOTICE",
             "log_message": "Certificate expires in 10 days"
             }
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]

    print(f"Send another batch of data: {batch2}\n")
    stream.process_stream(batch2)
    stream.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:\n")
    json_plugin = JsonExportPlugin()
    stream.output_pipeline(5, json_plugin)

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
