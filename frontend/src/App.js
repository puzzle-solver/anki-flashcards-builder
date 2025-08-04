import './App.css';


// Main App component
function App() {
  return (
  <div className="app-container">
        
    {/* Left Section - Input */}
    <div className="section section-left rounded-t-lg">
      <h2 className="title text-blue-600">
        Step 1: Input Data
      </h2>
      <p className="subtitle">
        Enter the required information to start the process.
      </p>
      <div className="input-group">
        <input 
          type="text" 
          placeholder="Enter value A" 
          className="input-field"
        />
        <input 
          type="text" 
          placeholder="Enter value B" 
          className="input-field"
        />
        <button className="action-button">
          Start Process
        </button>
      </div>
    </div>

    {/* Middle Section - Process */}
    <div className="section section-middle">
      <h2 className="title text-green-600">
        Step 2: Processing
      </h2>
      <p className="subtitle">
        Watch the magic happen as the process unfolds.
      </p>
      <div className="content-box">
        {/* Example of a dynamic state/loading indicator */}
        <div className="spin-loader"></div>
        <p className="processing-text">
          Processing data...
        </p>
      </div>
    </div>
        
    {/* Right Section - Output */}
    <div className="section section-right rounded-b-lg">
      <h2 className="title text-red-600">
        Step 3: Results
      </h2>
      <p className="subtitle">
        View the final output of your process.
      </p>
      <div className="content-box">
        <p className="output-value">
          123.45
        </p>
        <p className="output-label">
          Final Output Value
        </p>
      </div>
    </div>
  </div>
  );
};

export default App;
