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

With rainbows

```bash
$ gem install lolcat
$ cat service.log | gauge | lolcat
```

### How does `gauge` find the timestamps in a file with historical data?

`gauge` assumes your log entries start with a timestamp that is formatted by increasing specificity (year -> month -> day -> hour etc). This way we can simply group the log into historgram bars alphabetically.

If your log has a different format, you can use a tool like `awk` to reformat it:

```bash
cat service.log | awk '{print $2,$1}' | gauge
```

18:43:49 2020-04-14 ... -> 2020-04-14 18:43:49 ...




