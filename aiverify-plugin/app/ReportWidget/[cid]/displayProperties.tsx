export default function DisplayProperties({
  widget,
  properties,
  setProperties,
}) {
  if (!widget.meta || !widget.meta.properties) return <div></div>;

  const onChange = (key, event) => {
    setProperties({
      ...properties,
      [key]: event.target.value,
    });
  };

  return (
    <div className="text-left">
      {widget.meta.properties.map((prop) => (
        <div key={prop.key} style={{ marginTop: "10px" }}>
          <div className="font-bold" >{prop.key}</div>
          {prop.helper && <div>{prop.helper}</div>}
          <div>
            <input
              type="text"
              className="w-full border rounded p-1"
              value={properties[prop.key]}
              onChange={(e) => onChange(prop.key, e)}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
