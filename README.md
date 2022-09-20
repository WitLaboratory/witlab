<p align="center">
    <img width="400" height="160" src="#logo">
    <br>
    <a href="https://github.com/WitLaboratory/witlab/releases">
       <img alt="GitHub all releases" src="https://img.shields.io/github/downloads/WitLaboratory/witlab/total?color=yellow&label=Downloads%28Github%29">
    </a>
    <a href="https://pypi.org/project/witlab/">
        <img alt="PYPI" src="https://static.pepy.tech/personalized-badge/witlab?period=total&units=international_system&left_color=grey&right_color=yellow&left_text=Downloads(PYPI)">
    </a>
    
</p>

WitLab is a library intended to obtain, parse and analyze EEG, EMG, ECG, and other kinds of data from biosensors.

It provides a uniform SDK to work with biosensors with a primary focus on neurointerfaces, all features available for
free and distributed under MIT license.

#### Advantages of WitLab:

* powerful API with many features to simplify development
    * Straightforward API for data acquisition
    * Powerful API for signal filtering, denoising, downsampling...
    * Development tools like Synthetic board, Streaming board, logging API
* easy to use
    * WitLab has many bindings, you can choose programming language you like
    * All programming languages provide the same API, so it's simple to switch
    * API is uniform for all boards, it makes applications on top of WitLab almost board agnostic
* easy to support and extend
    * Code to read data and to perform signal processing is implemented only once in C/C++, bindings just call C/C++
      methods
    * Powerful CI/CD system which runs integrations tests for each commit automatically using WitLab's Emulator
    * Simplified process to add new boards and methods

## Resources

* [***WitLab Docs, Dev and User guides and other information***](https://WitLab.readthedocs.io)
* [***WitLab's slack workspace***](https://openbraintalk.slack.com/)***, use this*** [***link to
  join***](https://c6ber255cc.execute-api.eu-west-1.amazonaws.com/Express/)
* [***For WitLab Developers***](https://WitLab.readthedocs.io/en/master/WitLabDev.html)

## Contribution guidelines

If you want to contribute to WitLab, be sure to review
the [contribution guidelines](https://WitLab.readthedocs.io/en/stable/WitLabDev.html). This project adheres
to [WitLab's code of conduct](https://github.com/WitLab-dev/WitLab/blob/master/CODE_OF_CONDUCT.md). By
participating, you are expected to uphold this code.

We use [GitHub issues](https://github.com/WitLab-dev/WitLab/issues) for tracking requests and bugs, please use
WitLab's slack for general discussions.

The WitLab project strives to abide by generally accepted best practices in open-source software development.

## Build Status

|          Build Type            |                                                                                Status                                                                                |
|:---------------------------:	|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------:	|
|        Windows Tests            |   [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/WitLab-dev/WitLab/Run%20Windows/master?color=yellow&label=Windows%202019)](https://github.com/WitLab-dev/WitLab/actions/workflows/run_windows.yml)    |
| Unix(Linix and MacOS) Tests    | [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/WitLab-dev/WitLab/Run%20Unix/master?color=yellow&label=Ubuntu%20and%20MacOS)](https://github.com/WitLab-dev/WitLab/actions/workflows/run_unix.yml)    |
|        Android Tests            |   [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/WitLab-dev/WitLab/Run%20Android%20NDK/master?color=yellow&label=Android)](https://github.com/WitLab-dev/WitLab/actions/workflows/run_android.yml)    |
|         Alpine Tests            |       [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/WitLab-dev/WitLab/Run%20Alpine/master?color=yellow&label=Alpine)](https://github.com/WitLab-dev/WitLab/actions/workflows/run_alpine.yml)        |
|        Valgrind Tests        |     [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/WitLab-dev/WitLab/Run%20Valgrind/master?color=yellow&label=Valgrind)](https://github.com/WitLab-dev/WitLab/actions/workflows/valgrind.yml)        |
|           CppCheck            |    [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/WitLab-dev/WitLab/CppCheck/master?color=yellow&label=Static%20Analyzer)](https://github.com/WitLab-dev/WitLab/actions/workflows/cppcheck.yml)    |
|         Clang-Format            |   [![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/WitLab-dev/WitLab/Clang%20Format/master?color=yellow&label=Code%20Style)](https://github.com/WitLab-dev/WitLab/actions/workflows/clang_format.yml)    |  


## License:

[MIT](https://github.com/WitLab-dev/WitLab/blob/master/LICENSE)
