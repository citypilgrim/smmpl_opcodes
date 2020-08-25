# smmpl_opcodes

Operational code for scanning mini micropulse lidar

## Usage

### Running measurements

Running of measurement protocol; scripts titled as `<protocol name>_main.py`

```
python -m smmpl_opcodes
```
All protocols run the following services
1. Live status monitoring and notification (via Telegram)
2. Regular data moving and sync to solaris server
3. Measurement protocol

### Post measurement clean up

Can also be used to perform data organisation and sync; i.e. move data from SigmaMPL folder to data folders specified in params, and sync to solaris server

```
python -m smmpl_opcodes.sop
```

### Generate scan patterns

Timings of scan patterns can adjusted in the main script.

```
python -m smmpl_opcodes.scanpat_calc
```

### Getting current sun position

```
python -m smmpl_opcodes.scanpat_calc.sunforecaster
```