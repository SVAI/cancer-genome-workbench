import React, { Component } from 'react';
import { Col, Row, FormGroup, FormControl, ControlLabel, Button } from 'react-bootstrap';

var $ = require('jquery');

class Login extends Component{
  constructor(props) {
    super(props)
    this.state = {
      username: "",
      password: ""
    }
  }
  render() {
    const { username, password } = this.state;
    const { doLogin } = this.props;
    return (
      <Row>
        <Col md={3} className="panel panel-default center-block login-box">
          <form onSubmit={(e) => doLogin({username, password}, e)}>  
            <h3 className="text-center">Sign In</h3>
            <FormGroup>
              <ControlLabel>Username</ControlLabel>
              <FormControl
                type="text"
                placeholder="username"
                value={username}
                onChange={e => this.setState({username: e.target.value})}
                required={true}
              />
            </FormGroup>
            <FormGroup>
              <ControlLabel>Password</ControlLabel>
              <FormControl
                type="password"
                placeholder="password"
                value={password}
                onChange={e => this.setState({password: e.target.value})}
                required={true}  
              />
            </FormGroup>
            <Button type="submit" bsStyle="primary" block>Log in</Button>
          </form>  
        </Col>
      </Row>
    );
  }
};

export default Login;
