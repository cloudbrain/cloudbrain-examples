# Cloudbrain Examples

This repository consists mostly of a `README` with a list of examples as well as a series of JSON 
configurations files. The goal is to demonstrate how the different modules of CloudBrain work.

## Before you start
Make sure you have [CloudBrain](https://github.com/cloudbrain/cloudbrain) installed. 

```
cd <where you want to clone cloudbrain>
git clone https://github.com/cloudbrain/cloudbrain
cd cloudbrain
python setup.py develop --user
```

You can also refer to the [Setup](https://github.com/cloudbrain/cloudbrain/wiki/1.-Setup#setup) section of the [CloudBrain wiki](https://github.com/cloudbrain/cloudbrain/wiki) 


## Setting up `cloudbrain_examples`
If you want to be able to edit `cloudbrain_examples` without having to re-install the package, then run:
```
python setup.py develop --user
```

Otherwise, run:
```
python setup.py install --user
```

## Learn how to use CloudBrain's modules

All CloudBrain examples are under `cloudbrain_examples/modules`. CloudBrain modules can be chained together. 

<br>
Here is a very simple example
```
* --------------*   eeg    * --------------*  filtered_eeg   * --------------*
| OpenBCISource | ======>  |   BandFilter  | ==============> |   StdoutSink  |  (prints to console via stdout)
* --------------*          * --------------*                 * --------------*
         |
         |
         |        
         | eeg  * ----------------*  alpha   * --------------*
          ====> |   FFTTransform  | =======> |   PyPlotSink  | (plots live data via matplotlib.pyplot)
                * ----------------*          * --------------*
```

### Sources: modules sending data

Sources are the modules in charge of sending data to CloudBrain.
* `cloudbrain.sources.openbci.OpenBCISource`: send data from the OpenBCI to CloudBrain. 
* `cloudbrain.sources.openbci.MockSource`: send mock data to CloudBrain. 

#### Send mock data
To send mock data run: 
```
python -m cloudbrain.run --conf cloudbrain_examples/modules/sources/mock.json
```
Look at `cloudbrain_examples/modules/sources/mock.json` for more details about how the module is setup.

#### Send OpenBCI data
To send OpenBCI data run: 
```
python -m cloudbrain.run --conf cloudbrain_examples/modules/sources/openbci.json
```
> Tip: Make sure your OpenBCI board is connected and that the JSON conf file is using the right port.  

Look at `cloudbrain_examples/modules/sources/openbci.json` for more details about how the module is setup.

### Filters: modules filtering data

Filters are the modules in charge of filtering the data in CloudBrain.
* `cloudbrain.filters.band.BandFilter`: filter that can exclude frequencies (if `type = bandstop`) 
or keep only certain frequencies (if `type = bandpass`).

#### Band stop filter

To filter frequencies outside of a specified range run: 
```
python -m cloudbrain.run --conf cloudbrain_examples/modules/filters/band_stop.json
```
> Tip #1: You can edit the frequencies you filter out by editing `start_frequency` and `stop_frequency` in the JSON conf file.

Look at `cloudbrain_examples/modules/filters/band_stop.json` for more details about how the module is setup.

> Tip #2: You can use this filter to create a notch filter. Depending on your country the notch might be 50Hz or 60Hz. Say it is 60Hz; then you should filter out frequencies in the range `[59.0, 61.0]`.

#### Band pass filter

To keep only the frequencies in aspecified range run: 
```
python -m cloudbrain.run --conf cloudbrain_examples/modules/filters/band_pass.json
```
> Tip: You can edit the frequencies you keep by editing `start_frequency` and `stop_frequency` in the JSON conf file.

Look at `cloudbrain_examples/modules/filters/band_pass.json` for more details about how the module is setup.

### Sinks: getting data out of CloudBrain

Sinks are the modules in charge of relaying the data out of CloudBrain.
* `cloudbrain.sinks.stdout.StdoutSink`: write data to the console (stdout).
* `cloudbrain.sinks.pyplot.PyPlotSink`: plot a metric in real-time via `matplotlib.pyplot`.

#### Stdout sink: see CloudBrain's in the console

To write data to the console (stdout) run: 
```
python -m cloudbrain.run --conf cloudbrain_examples/modules/sinks/stdout.json
```
Look at `cloudbrain_examples/modules/sinks/stdout.json` for more details about how the module is setup.

> Tip: this module is useful to know if you are sending data to CloudBrain correctly with a `source`. Make sure that the settings are the same for `publishers` and `subscribers` in the modules that you are chaining (particularly, look at the `base_routing_key`, `metric_name` and `rabbitmq` address and credentials.

## Sandbox

In `cloudbrain_examples/sandbox` you will find snippets of code that might not be directly related to CloudBrain's 
modules. These snippets were often starting points to create new CloudBrain modules so I thought I would include them in the `cloudbrain_examples` repo.

### What's in `cloudbrain_examples/sandbox`?
* `plot_sine_wave.py`: plot data generated by CloudBrain's signal generator.
* `band_pass_filter.py`: experimentation with band pass filters + graphic comparison of the results.
* `plot_data_real_time.py`: code written to bootstrap the PyPlotSink module in CloudBrain.
* `print_data.py`: code written to bootstrap the StdoutSink module in CloudBrain.
* `send_sine_wave.py`: code written to bootstrap the MockSource module in CloudBrain.
* `send_basic_message.py`: just a mini demo of how the PikaPublisher works.

