# concurrent-echo-servers

A hands-on comparison of different concurrency models for a TCP echo server in Python. Each version accepts client connections on port 8000, echoes back whatever it receives, and demonstrates a different approach to handling multiple clients at once.

## Requirements

- Python >= 3.13
- [uv](https://docs.astral.sh/uv/) (this project uses `uv.lock` for dependency management)

## Setup

```bash
uv sync
```

This creates a virtual environment and installs the dependencies listed in `pyproject.toml`.

## Project structure

```text
app/
  v1_single_client.py   Blocking, single-client server (implemented)
  v2_select.py          I/O multiplexing with select() (planned)
  v3_threading.py        One thread per client connection (planned)
  v4_asyncio.py          Cooperative concurrency with asyncio (planned)
tests/
  client-simulator.py   CLI tool to spawn one or more test client connections
main.py                 Placeholder project entry point (uv scaffold)
```

### v1 — `app/v1_single_client.py`

The simplest possible echo server: a single blocking `accept()` / `recv()` loop.

- Listens on `0.0.0.0:8000`.
- Accepts one client, and blocks on that client's `recv()` until it disconnects, before accepting the next one.
- **By design, it can only serve one client at a time** — any other client that connects while one is already being served will hang until the first disconnects. This is the baseline the later versions (`select`, `threading`, `asyncio`) are meant to improve on.

### v2, v3, v4

Placeholder files for upcoming implementations exploring:

- `select()`-based I/O multiplexing (single-threaded, non-blocking)
- Thread-per-connection concurrency
- `asyncio`-based cooperative concurrency

Not yet implemented.

## Running a server

Start a server from the project root:

```bash
uv run python app/v1_single_client.py
```

You should see:

```text
Echo server listening on port 8000 ...
```

Leave it running in its own terminal.

## Testing with the client simulator

`tests/client-simulator.py` is a dependency-free TCP client for exercising a running echo server. In a second terminal:

```bash
uv run python tests/client-simulator.py hello world bye
```

This connects once, sends each word as a separate message, and prints what the server echoes back.

### Options

| Flag        | Default           | Description                                             |
| ----------- | ----------------- | ------------------------------------------------------- |
| `messages`  | `hello world bye` | Positional list of messages each client sends, in order |
| `--host`    | `127.0.0.1`       | Server host to connect to                               |
| `--port`    | `8000`            | Server port to connect to                               |
| `--clients` | `1`               | Number of concurrent client connections to spawn        |

### Simulating multiple concurrent clients

```bash
uv run python tests/client-simulator.py hi bye --clients 5
```

This spawns 5 client connections in parallel threads, each sending the same messages and printing its own `[client N]`-tagged output.

Running this against `v1_single_client.py` is a good way to *see* its single-client limitation: connections queue up and are served strictly one at a time, rather than concurrently. Later server versions are expected to handle this case without serializing clients.

> **Note:** Make sure a server is running before starting the simulator — `ConnectionRefusedError` / `WinError 10061` means nothing is listening on the target host/port yet.

## Stopping a server

Press `Ctrl+C` in the terminal running the server.
