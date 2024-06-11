import React, { useEffect, useState, useRef } from "react";
import ReactDOM from "react-dom/client";
import "./styles.css";
import Headers from "./Components/headers";
import Footer from "./Components/footer";
import Section from "./Components/section";
import { initializeFaro } from './faro';

function Body() {
  // const faroRef = useRef(null);
  const [itemNum, setItemNum] = useState(0);
  const [displayMode, setDisplayMode] = useState("all");
  const [footerDisplay, setFooterDisplay] = useState(false);

  useEffect(() => {
    if (!footerDisplay) setDisplayMode("all");
  }, [footerDisplay]);

  const faroRef = useRef(null);
  useEffect(() => {
    if (!faroRef.current) {
      faroRef.current = initializeFaro()
    }
  }, [])
  
  return (
    <React.StrictMode>
      <div style={{ display: 'flex', justifyContent: 'center'}}>
        <div style={{ width: "60%" }}>
          <Headers />
          <Section
            editNum={setItemNum}
            mode={displayMode}
            displayTask={setFooterDisplay}
          />
          {footerDisplay ? (
            <Footer num={itemNum} editMode={setDisplayMode} />
          ) : (
            <></>
          )}
        </div>
      </div>
    </React.StrictMode>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<Body />);
