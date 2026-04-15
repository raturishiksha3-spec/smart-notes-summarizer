import React from "react";

function App() {
  return (
    <div className="bg-gray-100 border-border min-h-screen p-6">
      <header className="max-w-3xl mx-auto text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-800">Smart Notes Summarizer</h1>
        <p className="text-gray-600 mt-2">
          Summarize and organize your notes quickly with AI
        </p>
      </header>

      <main className="max-w-3xl mx-auto bg-white shadow-md rounded-lg p-6 space-y-4">
        <textarea
          className="w-full border border-gray-300 rounded-md p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows="6"
          placeholder="Paste your notes here..."
        ></textarea>

        <button className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 px-4 rounded-md">
          Summarize Notes
        </button>

        <div className="border border-gray-200 rounded-md p-4 bg-gray-50">
          <h2 className="font-semibold text-gray-700 mb-2">Summary</h2>
          <p className="text-gray-600">
            Your summarized notes will appear here after clicking the button.
          </p>
        </div>
      </main>

      <footer className="max-w-3xl mx-auto text-center mt-12 text-gray-500 text-sm">
        &copy; 2025 Smart Notes Summarizer
      </footer>
    </div>
  );
}

export default App;
