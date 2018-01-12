
import React, { Component } from 'react';
import logo from './logo.svg';
import { Grid, Row, Col } from 'react-flexbox-grid';
import './StatusHeader.css';

class StatusHeader extends Component {

    constructor(props) {
        super(props);
        var data = {};
        props.fields.forEach( (fieldName) => {
            data[fieldName.toLowerCase()] = ["unknown", "yellow"]
        });
        this.state = {data: data};
    }

    loadData() {
        fetch("/api/system_status")
            .then(response => response.json())
            /* This shoud lowercase the status keys first */
            .then(data => {this.setState({data: data }) })
            .catch(err => console.error(this.props.url, err.toString()))
    }

    componentDidMount() {
            this.loadData()
    }

    render() {
      /* Need error checking for when the field name doesn't exist */
        return (
        <header className="StatusHeader">
          <Grid>
            <Row>
              <Col md={2}>
                  <img src={logo} className="Header-logo" alt="logo" />
                  <h1 className="Header-title">ZTF Alerts</h1>
              </Col>
              <Col md={6}>
              { this.props.fields.map( fieldName => (
                  <p key={fieldName}>{fieldName}: &nbsp;
                    <font color={this.state.data[fieldName.toLowerCase()][1]}> 
                      {this.state.data[fieldName.toLowerCase()][0] }
                    </font>
                  </p>
              )
              )}
              </Col>
            </Row>
          </Grid>
        </header>
     );
    }
}

export default StatusHeader;
