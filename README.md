# txt2pid

Extract a list of identifiers from text.

For example, using the cli to output json-lines:

```
curl -s "https://sis.web.cern.ch/submit-and-publish/persistent-identifiers/pids-for-objects" | \
  pandoc -s -r html -t plain | \
  python -m txt2pid

{"offset": 14226, "source": "ark:'", "scheme": "ark", "content": "'"}
{"offset": 14567, "source": "ark:/13030/tf5p30086k", "scheme": "ark", "content": "13030/tf5p30086k"}
{"offset": 15033, "source": "arXiv:1207.7214", "scheme": "arXiv", "content": "1207.7214"}
{"offset": 15929, "source": "10.23731/CYRM-2019-007", "scheme": "doi", "content": "10.23731/CYRM-2019-007"}
{"offset": 15986, "source": "10.7483/OPENDATA.CMS.6O84.WLN8", "scheme": "doi", "content": "10.7483/OPENDATA.CMS.6O84.WLN8"}
{"offset": 16037, "source": "10.5281/zenodo.821635", "scheme": "doi", "content": "10.5281/zenodo.821635"}
{"offset": 16081, "source": "10.1016/j.physletb.2012.08.020", "scheme": "doi", "content": "10.1016/j.physletb.2012.08.020"}
{"offset": 17060, "source": "hdl:2381/12775", "scheme": "hdl", "content": "2381/12775"}
{"offset": 18819, "source": "urn:isbn:0451450523", "scheme": "isbn", "content": "0451450523"}
```
