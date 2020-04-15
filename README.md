![pipe-gauge](gauge.py)

# pipe-gauge

Quickly turn logs into time-series histograms in your terminal.

## Installation 

TODO

## Usage

Graph a file with historical data:

`$ cat service.log | gauge`

Graph a real-time stream:

`$ tail -f service.log | gauge -f`

With rainbows:

`$ gem install lolcat`
`$ cat service.log | gauge | lolcat`

### How does `gauge` find the timestamp in a file with historical data?

`gauge` assumes your log starts with a timestamp that is formatted by increasing specificity (year -> month -> day -> hour etc). This way we can simply group the log into historgram bars alphabetically.

If your log has a different format, you can use a tool like `awk` to reformat it:

`$ cat service.log | awk '{print $2,$1}' | gauge`

18:43:49 2020-04-14 ... -> 2020-04-14 18:43:49 ...




