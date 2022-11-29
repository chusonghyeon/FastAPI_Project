import React, { useEffect, useState} from "react";

import Register from "./components/Register";
import Header from "./components/Header";
import Login from "./components/Login";
import Table from "./components/Table";


import { useContext } from "react";
import { UserContext } from "./context/UserContext";

const App = () => {
  const [message, setMessage] = useState("");
  const [token] = useContext(UserContext)

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await fetch("/api", requestOptions);
    const data = await response.json();

    // console.log(data);
    if (!response.ok) {
      console.log("somethong messed up")
    } else {
      setMessage(data.message);
    }
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);

  return (
    <>
      <Header title={message} />
      <div className="columns">
        <div className="column"></div>
        <div className="column m-5 is-two_thirds">
          {!token ? (
              <div className="columns">
                <Register/> <Login />
              </div>
            ) : (
              <Table />
            )}
        </div>
        <div className="column"></div>
      </div>
    </>
  );
};

export default App;
