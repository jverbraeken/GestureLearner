# coding=utf-8

system, udp_scanner, ui, grt_writer, byte_stream_interpreter = range(5)
loggers = {}


def register(service_locator, logging_disabled):
    class Dummy:
        class LoggingDisabledException(Exception):
            pass

        def always(self, message):
            raise self.LoggingDisabledException("Log statement executed while debug mode is diabled")

        def error_always(self, message):
            raise self.LoggingDisabledException("Log statement executed while debug mode is diabled")

        def warning_always(self, message):
            raise self.LoggingDisabledException("Log statement executed while debug mode is diabled")

        def user_input(self, message):
            raise self.LoggingDisabledException("Log statement executed while debug mode is diabled")

        def user_input_response(self, message):
            raise self.LoggingDisabledException("Log statement executed while debug mode is diabled")

        def error(self, message):
            raise self.LoggingDisabledException("Log statement executed while debug mode is diabled")

        def warning(self, message):
            raise self.LoggingDisabledException("Log statement executed while debug mode is diabled")

        def message(self, message):
            raise self.LoggingDisabledException("Log statement executed while debug mode is diabled")

        def comment(self, message):
            raise self.LoggingDisabledException("Log statement executed while debug mode is diabled")

    if logging_disabled:
        loggers.update({system: Dummy})
        loggers.update({udp_scanner: Dummy})
        loggers.update({ui: Dummy})
        loggers.update({grt_writer: Dummy})
        loggers.update({byte_stream_interpreter: Dummy})
    else:
        loggers.update({system: service_locator.logger_factory.get_logger(system)})
        loggers.update({udp_scanner: service_locator.logger_factory.get_logger(udp_scanner)})
        loggers.update({ui: service_locator.logger_factory.get_logger(ui)})
        loggers.update({grt_writer: service_locator.logger_factory.get_logger(grt_writer)})
        loggers.update({byte_stream_interpreter: service_locator.logger_factory.get_logger(byte_stream_interpreter)})

def getLogNameFromID(logID):
    return {
        system: "system",
        udp_scanner: "udp_scanner",
        ui: "ui",
        grt_writer: "grt_writer",
        byte_stream_interpreter: "byte_stream_interpreter"
    }.get(logID, "undefined")
