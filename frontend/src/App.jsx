
import { useState } from "react";
import { Editor } from "ketcher-react";
import { StandaloneStructServiceProvider } from "ketcher-standalone";
import "ketcher-react/dist/index.css";

const structureService = new StandaloneStructServiceProvider();

function App() {
    const [ketcher, setKetcher] = useState(null);
    const [result, setResult] = useState("");
    const [loading, setLoading] = useState(false);

    async function getIupacName() {
        if (!ketcher) return;

        setLoading(true);
        setResult("");

        try {
            const smiles = await ketcher.getSmiles();

            if (!smiles) {
                setResult("Please draw a compound first.");
                return;
            }

            const response = await fetch("/get-iupac", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ smiles }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || "Could not identify compound.");
            }

            setResult(data.iupac_name);
        } catch (error) {
            setResult(error.message || "Something went wrong.");
        } finally {
            setLoading(false);
        }
    }

    return (
        <div style={{ padding: "20px", fontFamily: "Arial" }}>
            <h1>Organic Nomenclature</h1>
            <p>Draw your organic compound below.</p>

            <div style={{ height: "600px", width: "100%" }}>
                <Editor
                    staticResourcesUrl={import.meta.env.BASE_URL}
                    structServiceProvider={structureService}
                    onInit={setKetcher}
                    disableMacromoleculesEditor
                />
            </div>

            <button
                onClick={getIupacName}
                disabled={!ketcher || loading}
                style={{ marginTop: "20px", padding: "12px" }}
            >
                {loading ? "Identifying..." : "Get IUPAC Name"}
            </button>

            {result && (
                <div>
                    <h2>Result</h2>
                    <p>{result}</p>
                </div>
            )}
        </div>
    );
}

export default App;
