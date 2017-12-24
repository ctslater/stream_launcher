
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
            <div>
            <Row className="PodCard">
              <Col md={3}><button onClick={this.toggleExpand}>{this.props.pod.name}</button></Col>
              <Col md={2}>{this.props.pod.node}</Col>
              <Col md={1}>{this.props.pod.status}</Col>
              <Col md={1}>{this.props.pod.running_time}</Col>
            </Row>
            { this.state.expanded ? (
            <Row className="PodCard">
              <Col md={4}>
                <ul>
                  <li>Image: {this.props.pod.image}</li>
                  <li>Restarts: {this.props.pod.restarts}</li>
                </ul>
              </Col>
              <Col md={2}><button>Terminate Filter</button></Col>
            </Row>
            ) : null }
            </div>

       );
    }
}

class NewFilterCard extends PodCard {
    render() {
        return (
            <Row className="PodCard">
            { !this.state.expanded ? (
              <Col md={3}><button onClick={this.toggleExpand}>Add new filter</button></Col>
            ) : (
   <Col md={4}>
    <p>Filter name: <input type="text" name="filter_name" /></p>
    <p>Filter type: <input type="text" name="filter_name" /></p>
    <p>Filter string: <input type="text" name="filter_string" /></p>
    <p><button>Add Filter</button> <button>Cancel</button></p>
   </Col>
            ) }
            </Row>
       );
    }
}

class PodHeader extends Component {
    render() {
        return (
            <Row className="PodHeader">
              <Col md={3}>Name</Col>
              <Col md={2}>Node</Col>
              <Col md={1}>State</Col>
              <Col md={1}>Age</Col>
            </Row>
       );
    }
}

class PodList extends Component {

    constructor(props) {
        super(props);
        this.state = {};
        this.state.pods = [];
    }

    loadData() {
        fetch("/api/pods")
            .then(response => response.json())
            /* Probably should add some validation here */
            .then(data => {this.setState({pods: data }) })
            .catch(err => console.error(this.props.url, err.toString()))
    }

    componentDidMount() {
            this.loadData()
    }

    render() {
        return (
            <Grid fluid className="PodList">
              <PodHeader />
              {this.state.pods.map(function(pod, i) {
                return <PodCard pod={pod} />;
                  }
              )}
              <NewFilterCard />
            </Grid>
       );
    }
}

export default PodList;

