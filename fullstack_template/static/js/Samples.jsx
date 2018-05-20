import React, { Component } from 'react';
var $ = require('jquery');

class Samples extends Component{
  constructor(props) {
    super(props)
    this.state = {
      samples: [],
      variants: [],
      scores: [],
      sample_selected: ''
    }
  }
  componentDidMount() {
    this.getSamples();
  }
  getSamples() {
    const _t = this;
    $.post('/samples', (data) => {
      _t.setState(data[1]);
    }, "json");
  }
  handleSelectSample(event, sampleId, sampleObject) {
    this.setState({ sample_selected: sampleObject })
    const element = event.currentTarget;
    const radioElement = $(element).find("input[type='radio']")[0];
    if (!radioElement.checked) {
      this.getVariantsBySample(sampleId)
      this.getScoresBySample(sampleId)
    }
    
    radioElement.checked = true
  }
  getVariantsBySample(sampleId) {
    const _t = this;
    $.post('/variants', { sampleid: sampleId }, (data) => {
      _t.setState(data[1]);
    }, "json");
  }
  getScoresBySample(sampleId) {
    const _t = this;
    $.post('/scores', { sampleid: sampleId }, (data) => {
      _t.setState(data[1]);
    }, "json");
  }
  render() {
    const { samples, variants, scores, sample_selected } = this.state;
    const samplesRows = samples.map((sample) => {
      const { sampleid, name, relationship, status, updated, created } = sample;
      const isActive = sample_selected.sampleid === sampleid
        ? 'info'
        : ''
      return (
        <tr key={`sample_key_${sampleid}`} className={`${isActive}`} onClick={(e) => this.handleSelectSample(e, sampleid, sample)}>
          <td><input type="radio" name="sample_radio"/></td>
          <td>{name}</td>
          <td>{relationship}</td>
          <td>{status}</td>
          <td>{updated}</td>
          <td>{created}</td>
        </tr>
      );
    });
    
    const variantsRows = variants.map((variant) => {
      const { samplename, id, chrom, pos, het, reads, zygosity, databases, previouslyseen } = variant;
      return (
        <tr key={`variant_key_${id}`}>
          <td>{samplename}</td>
          <td>{id}</td>
          <td>{chrom}</td>
          <td>{pos}</td>
          <td>{het}</td>
          <td>{reads}</td>
          <td>{zygosity}</td>
          <td>{databases}</td>
          <td>{previouslyseen}</td>
        </tr>
      );
    });

    const scoreRows = scores.map((item) => {
      const { scoreid, score, disease, treatment } = item;
      return (
        <tr>
          <td>{scoreid}</td>
          <td>{score}</td>
          <td>{disease}</td>
          <td>{treatment}</td>
        </tr>
      );
    });
    return (
      <div className="col-sm-12">
        <div className="row">
          <header id="sample_header" className="col-sm-12">
            <span className="btn btn-link pull-right" onClick={this.props.doLogOut}><b>Logout</b></span>
          </header>
          <div className="col-sm-12">
            <ul className="nav nav-pills">
              <li className="active"><a href="#">Samples</a></li>
              <li className="pull-right"><a href="#" className="btn btn-default">ADD SAMPLE</a></li>
            </ul>
          </div>
          <div className="col-sm-12">
            <table id="samples_table" className="table table-bordered table-hover table-striped table-condensed">
              <thead>
                <tr>
                  <th></th>
                  <th>Sample</th>
                  <th>Family</th>
                  <th>Status</th>
                  <th>Updated</th>
                  <th>Created</th>
                </tr>
              </thead>
              <tbody>
                {samplesRows}
              </tbody>
            </table>
          </div>
          <div className="col-sm-12">
            <ul className="nav nav-pills">
              <li className="active"><a href="#">Variants</a></li>
              <li><a href="#">Genes</a></li>
              <li><a href="#">Panels</a></li>
              <li><a href="#">Phenotypes</a></li>
            </ul>
          </div>
          <div className="col-sm-12">
            <table className="table table-bordered table-hover table-striped table-condensed">
              <thead>
                <tr>
                  <th>Sample</th>
                  <th>ID</th>
                  <th>CHROM</th>
                  <th>POS</th>
                  <th>Het</th>
                  <th>Reads</th>
                  <th>Zygosity</th>
                  <th>Databases</th>
                  <th>Prev. Seen</th>
                </tr>
              </thead>
              <tbody>
                {variantsRows}
              </tbody>
            </table>
          </div>
          {sample_selected && (
            <div>
              <div className="col-sm-6">
                <img className="img-thumbnail img-responsive col-sm-10 vcenter" src={`dist/plot${sample_selected.sampleid}.png`} alt="sample_graphic_image" />
                <div className="col-sm-2 vcenter">
                  <span className="glyphicon glyphicon-plus"></span>
                  <span className="glyphicon glyphicon-minus"></span>
                </div>
              </div>
              <div className="col-sm-6">
                <table className="table table-bordered table-hover table-striped table-condensed">
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Score</th>
                      <th>Disease</th>
                      <th>Treatment</th>
                    </tr>
                  </thead>
                  <tbody>
                    {scoreRows}
                  </tbody>
                </table>
              </div>
            </div>
            )}
        </div>
      </div>
    );
  }
}
export default Samples;