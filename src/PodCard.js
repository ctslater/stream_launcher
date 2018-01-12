
import React, { Component } from 'react';
import { Grid, Row, Col } from 'react-flexbox-grid';
import './PodList.css';

class PodCard extends Component {
    constructor(props) {
        super(props);
        this.state = {
            expanded: false,
        };
        this.toggleExpand = this.toggleExpand.bind(this);
    }

    toggleExpand(e) {
        e.stopPropagation();
        this.setState({expanded: !this.state.expanded})
    }

    render() {
        return (
            <div className="CardContainer">
            <Row className="PodCard">
              <Col md={3}><button onClick={this.toggleExpand}>{this.props.pod.name}</button></Col>
              <Col md={2}>{this.props.pod.node}</Col>
              <Col md={1}>{this.props.pod.status}</Col>
              <Col md={1}>{this.props.pod.running_time}</Col>
            </Row>
            { this.state.expanded ? (
            <Row className="PodCard SelectedCardDetail">

              <Col md={8}>
                <Grid className="PodDetail">
                  <Row className="PodDetailHeader">
                    <Col md={6}>Image</Col>
                    <Col md={6}>Restarts</Col>
                  </Row>
                  <Row>
                    <Col md={6}>{this.props.pod.image}</Col>
                    <Col md={6}>{this.props.pod.restarts}</Col>
                  </Row>
                  <Row>
                    <Col md={6}>&nbsp;</Col>
                    <Col md={6}>&nbsp;</Col>
                  </Row>
                  <Row>
                    <Col md={6}><button>Terminate Filter</button></Col>
                    <Col md={6}></Col>
                  </Row>
                </Grid>

              </Col>
            </Row>
            ) : null }
            </div>

       );
    }
}
export default PodCard;
