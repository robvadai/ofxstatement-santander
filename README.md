OFX Statement Santander plugin
==============================

![Workflow Status](https://github.com/robvadai/ofxstatement-santander/actions/workflows/test.yaml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/robvadai/ofxstatement-santander/badge.svg?branch=main)](https://coveralls.io/github/robvadai/ofxstatement-santander?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Summary

Converts Santander transaction files to [Open Financial Exchange (OFX)](https://en.wikipedia.org/wiki/Open_Financial_Exchange) format.

It is a plugin for [ofxstatement](https://github.com/kedder/ofxstatement).

At the moment it only supports converting [Quicken Interchange Format (QIF)](https://en.wikipedia.org/wiki/Quicken_Interchange_Format) files to OFX for Santander United Kingdom bank accounts.

This plugin also installs the [OFX Statement QIF plugin](https://github.com/robvadai/ofxstatement-qif), because it relies on its functionality.

## Installation

```shell
pip install ofxstatement-santander
```

## Usage

```shell
ofxstatement convert -t santander-uk-qif transactions.qif transactions.ofx
```

## Configuration

```shell
ofxstatement edit-config
```

And enter e.g. this:
```ini
[santander-uk-qif]
plugin = santander-uk-qif
currency = GBP
account = Quiffen Default Account
separator = \n
day-first = true
encoding = utf-8
```