
# Chronos

Tracing on steroids.

# Introduction

Chronos is a logging and signal recording and viewing tool. It is intended
to analyze systems behavior. It is very suited for dealing with systems
over time and analyzing their behaviors.

Examples of timestamped data:

- Measurements (cpu usage, voltages measured by DAQ cards)
- Video (camera streams)
- Audio (microphone measurements)
- Log messages
- Tracing data from DTrace / systemtap

# Installation

Create a virtualenv with the required packages in it:

  $ virtualenv myenv
  $ source myenv/bin/activate
  $ pip install -r requirements

# Usage

To start the GUI, use:

```shell
$ python -m chronos
```

# Development

[![Build Status](https://travis-ci.org/windelbouwman/chronos.svg?branch=master)](https://travis-ci.org/windelbouwman/chronos)

[![Build status](https://ci.appveyor.com/api/projects/status/cj1m66gmbfdv4td3?svg=true)](https://ci.appveyor.com/project/WindelBouwman/chronos)

