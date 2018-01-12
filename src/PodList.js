
import React, { Component } from 'react';
import { Grid, Row, Col } from 'react-flexbox-grid';
import PodCard from './PodCard.js';
import NewFilterCard from './NewFilterCard.js';
import './PodList.css';



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
                return <PodCard key={pod.name} pod={pod} />;
                  }
              )}
              <NewFilterCard />
            </Grid>
       );
    }
}

export default PodList;

