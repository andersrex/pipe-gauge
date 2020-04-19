<p align="center">
  <a href="https://github.com/andersrex/pipe-gauge">
    <img src="https://github.com/andersrex/pipe-gauge/raw/master/gauge.png" width="260"/>
  </a>
</p>

# pipe-gauge

> Quickly turn logs into time-series histograms in your terminal.

<img src="https://github.com/andersrex/pipe-gauge/raw/master/screenshot.png" width="520" />


## Installation 

```bash
cat https://github.com/andersrex/pipe-gauge/raw/master/gauge.py > gauge
chmod 744 gauge
```

## Usage

Graph a file with historical data
```bash
cat service.log | gauge
```

Graph a real-time stream
```bash
tail -f service.log | gauge -f
```

Graph a real-time stream with a custom time interval (10 sec)
```bash
tail -f service.log | gauge -f -i 10s
```

With rainbows

```bash
$ gem install lolcat
$ cat service.log | gauge | lolcat
```

### How does `gauge` find the timestamps in a file with historical data?

`gauge` uses `dateutil.parser` to try to find a timestamp on each row of input data. If your input data contains multiple timestamps per row or numerical data that confuses `dateutil.parser`, you can try using a tool like awk to narrow down you selection:

`2020-04-19 16:21:41 localhost: BackgroundAction scheduled: 2020-04-19 17:00:00`

⇩

```bash
cat service.log | awk '{print $1,$2}' | gauge
```

⇩

`2020-04-19 16:21:41`



