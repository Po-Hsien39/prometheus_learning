import { useState } from "react"
function Footer(props){
    const [mode, setMode] = useState({'all': true, 'active': false, 'complete': false})
    const changeMode = (currentMode)=>{
        props.editMode(currentMode)
        let tempMode = mode;
        for(const[key, value] of Object.entries(mode)){
            (currentMode === key)?(tempMode[key] = true):(tempMode[key] = false)
        }
        setMode(tempMode)
    }
    const style = {'backgroundColor': '#333', "color": "white"}
    const initialStyle = {'backgroundColor': '#fff', "color": "#333"}
    return (<footer className="todo-app__footer" id="todo-footer">
            <div className="todo-total">{props.num} left</div>
                <ul className="todo-app__view-buttons">
                    <button id="show-all" onClick={()=>changeMode('all')} style={mode['all']?style:initialStyle}>All</button>
                    <button id="show-active" onClick={()=>changeMode('active')} style={mode['active']?style:initialStyle}>Active</button>
                    <button id="show-complete" onClick={()=>changeMode('complete')} style={mode['complete']?style:initialStyle}>Completed</button>
                </ul>
                <div className="todo-app__clean">
                    <button onClick={()=>props.editMode('delete')}>Clear Completed</button>
                </div>
        </footer>)
}

export default Footer;