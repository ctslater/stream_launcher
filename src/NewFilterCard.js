
import React from 'react';
import { Grid, Row, Col } from 'react-flexbox-grid';
import PodCard from './PodCard.js';
import './PodList.css';

class NewFilterCard extends PodCard {
    constructor(props) {
        super(props);
        this.colwidth = 4;
        this.state = {images: [],
                      filter_name: "",
                      image_name: ""};

        this.handleFilterNameChange = this.handleFilterNameChange.bind(this);
        this.handleImageChange = this.handleImageChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    loadData() {
        fetch("/api/images")
            .then(response => response.json())
            /* Probably should add some validation here */
            .then(data => {
                    this.setState({images: data, image_name: data[0].name})
            })
            .catch(err => console.error(this.props.url, err.toString()));

        /* this.setState({image_name: this.state.images[0].image_name}); */
    }

    componentDidMount() {
            this.loadData()
    }

    handleFilterNameChange(event) {
        this.setState({filter_name: event.target.value});
    }

    handleImageChange(event) {
        this.setState({image_name: event.target.value});
    }

    handleSubmit(event) {
        fetch("/api/startPod", {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json' },
            body: JSON.stringify({
                filter_name: this.state.filter_name,
                image_name: this.state.image_name, })
            });
        event.preventDefault();
    }

    render() {
        return (
            <Row className="PodCard">
            { !this.state.expanded ? (
              <Col md={3}><button onClick={this.toggleExpand}>Add new filter</button></Col>
            ) : (
              <Col md={8}>
                <Grid className="PodDetail">
                <form onSubmit={this.handleSubmit}>
                  <Row className="PodDetailHeader">
                    <Col md={this.colwidth}>Filter Name</Col>
                    <Col md={this.colwidth}>Image</Col>
                  </Row>
                  <Row>
                    <Col md={this.colwidth}>
                        <input type="text" name="filter_name"
                               value={this.state.filter_name}
                               onChange={this.handleFilterNameChange} />
                    </Col>
                    <Col md={this.colwidth}>
                        <select name="image" value={this.state.image_name}
                                onChange={this.handleImageChange} >
                            {this.state.images.map(function(image, i) {
                            return <option value={image.name} key={image.name}>
                                    {image.name}
                                    </option>
                            })}
                        </select>
                    </Col>
                  </Row>
                  <Row className="PodDetailHeader">
                    <Col md={this.colwidth}>Input Topic</Col>
                    <Col md={this.colwidth}>Output Topic</Col>
                  </Row>
                  <Row>
                    <Col md={this.colwidth}>
                        <select name="input_topic">
                            <option value="public">ZTF Public</option>
                            <option value="collab">ZTF Collaboration</option>
                            <option value="caltech">ZTF Caltech</option>
                        </select>
                    </Col>
                    <Col md={this.colwidth}><input type="text" name="output_topic" /></Col>
                  </Row>
                  <Row>
                    <Col md={this.colwidth}>&nbsp;</Col>
                    <Col md={this.colwidth}>&nbsp;</Col>
                  </Row>
                  <Row>
                    <Col md={this.colwidth}><input type="submit" value="Create Filter"/></Col>
                    <Col md={this.colwidth}><button onClick={this.toggleExpand}>Cancel</button></Col>
                  </Row>
                </form>
                </Grid>
              </Col>
            ) }
            </Row>
       );
    }
}
export default NewFilterCard;
