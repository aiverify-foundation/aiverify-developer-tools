export default function DisplayProperties ({ widget, properties, setProperties }) {
  if (!widget.meta || !widget.meta.properties)
    return <div></div>;

  const onChange = (key, event) => {
    setProperties({
      ...properties,
      [key]: event.target.value,
    })
  }

  return (
    <div style={{ marginTop:'10px', padding:'10px', color:'#676767', textAlign:'left' }}>
      {widget.meta.properties.map(prop => (
        <div key={prop.key} style={{ marginTop:'10px' }}>
          <div style={{ fontWeight:'600' }}>{prop.key}</div>
          {prop.helper && <div>{prop.helper}</div>}
          <div><input type="text" style={{ width:'100%'}} value={properties[prop.key]} onChange={(e) => onChange(prop.key, e)} /></div>
        </div>
      ))}
    </div>
  )
}