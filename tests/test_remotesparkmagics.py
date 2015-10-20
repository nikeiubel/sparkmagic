from nose.tools import raises, with_setup
from mock import MagicMock

from remotespark.RemoteSparkMagics import RemoteSparkMagics


ip = get_ipython()
magic = None
spark_controller = None


def _setup():
    global magic, spark_controller
    magic = RemoteSparkMagics(shell=ip)
    ip.register_magics(magic)

    spark_controller = MagicMock()
    magic.spark_controller = spark_controller


def _teardown():
    pass


@with_setup(_setup, _teardown)
def test_info_command_parses():
    print_info_mock = MagicMock()
    magic._print_info = print_info_mock
    command = "info"

    ip.run_line_magic("spark", command)

    print_info_mock.assert_called_once_with()


@with_setup(_setup, _teardown)
def test_add_endpoint_command_parses():
    add_endpoint_mock = MagicMock()
    spark_controller.add_endpoint = add_endpoint_mock
    command = "add"
    name = "name"
    language = "python"
    connection_string = "url=http://location:port;username=name;password=word"
    line = " ".join([command, name, language, connection_string])

    ip.run_line_magic("spark", line)

    add_endpoint_mock.assert_called_once_with(name, language, connection_string)


@with_setup(_setup, _teardown)
def test_delete_endpoint_command_parses():
    mock_method = MagicMock()
    spark_controller.delete_endpoint = mock_method
    command = "delete"
    name = "name"
    line = " ".join([command, name])

    ip.run_line_magic("spark", line)

    mock_method.assert_called_once_with(name)


@with_setup(_setup, _teardown)
def test_mode_command_parses():
    mock_method = MagicMock()
    spark_controller.set_log_mode = mock_method
    command = "mode"
    mode = "debug"

    line = " ".join([command, mode])

    ip.run_line_magic("spark", line)

    mock_method.assert_called_once_with(mode)


@with_setup(_setup, _teardown)
def test_cleanup_command_parses():
    mock_method = MagicMock()
    spark_controller.cleanup = mock_method
    command = "cleanup"

    ip.run_line_magic("spark", command)

    mock_method.assert_called_once_with()


@raises(ValueError)
@with_setup(_setup, _teardown)
def test_bad_command_throws_exception():
    command = "bad_command"

    ip.run_line_magic("spark", command)


@with_setup(_setup, _teardown)
def test_run_cell_command_parses():
    mock_method = MagicMock()
    spark_controller.run_cell = mock_method
    command = "-c"
    name = "endpoint_name"
    line = " ".join([command, name])
    cell = "cell code"

    ip.run_cell_magic("spark", line, cell)

    mock_method.assert_called_once_with(name, False, cell)
