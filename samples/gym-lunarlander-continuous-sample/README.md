# OpenAI Gym Lunar Lander Continuous Sample

## SWIG INSTALLATION
* **OSX**
  * brew install swig
* **Ubuntu**
  * apt-get install -y swig
* **Windows**
  * Download swigwin zip package from the [SWIG website](http://www.swig.org/) and unzip. Add the unzipped folder to your system $PATH variable. (Microsoft Visual C++14 is required)
  * Anaconda users can run `conda install -c anaconda swig`

## Running simulator
Simulators need two environment variables set to be able to attach to the platform.

The first is `SIM_ACCESS_KEY`. You can create one from the `Account Settings` page.
You have one chance to copy the key once it has been created. Make sure you don't enter
the ID.

The second is `SIM_WORKSPACE`. You can find this in the URL after `/workspaces/` once
you are logged in to the platform.

There is also an optional `SIM_API_HOST` key, but if it is not set it will default to `https://api.bons.ai`.

If you're launching your simulator from the command line, make sure that you have these two
environment variables set. If you like, you could use the following example script:

```sh
export SIM_WORKSPACE=<your-workspace-id>
export SIM_ACCESS_KEY=<your-access-key>
python3 lunarlander_continuous_simulator.py
```

## Questions about Inkling?
See our [Inkling Guide](http://docs.bons.ai/guides/inkling-guide.html) and [Inkling Reference](http://docs.bons.ai/references/inkling-reference.html) for help.
