import React from "react";
import Login from "./Login";
import Samples from './Samples';
import '../css/fullstack.css';

var $ = require('jquery');

export default class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            login: false
        };
    }
    componentWillMount() {
        this.checkSession();
    }
    checkSession() {
        var session = sessionStorage.getItem('session');
        session && this.setState({ login: session });
        console.log(session)
    }
    doLogin({ username, password }, e) {
        e.preventDefault();
        const _t = this;
        $.post('/login', { username, password }, (data) => {
            if (data[1].login) {
                _t.setState(data[1]);
                sessionStorage.setItem('session', 'true');
            }
        }, "json");
    }
    doLogOut() {
        var session = sessionStorage.getItem('session');
        if (session) {
            sessionStorage.setItem('session', '');
            this.setState({ login: false });
        }
    }
    render() {
        const { login } = this.state;
        return (
            <div className="container">
                {login
                    ? <Samples doLogOut={this.doLogOut.bind(this)}/> 
                    : <Login doLogin={this.doLogin.bind(this)} />}
            </div>
        );
    }
}
