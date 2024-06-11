import { useState, useEffect } from "react";

function TodoItem(props){
    const [display, setDisplay] = useState('flex')
    const [complete, setComplete] = useState(false)
    const deleteTodo = ()=>{
        setDisplay('none')
        props.deleteNum(props.length)
    }
    const modifyComplete = ()=>{
        props.modify(props.length)
        setComplete(!complete)
    }
    useEffect(()=>{
        if (props.status)
            setDisplay('none')
        else
            setDisplay('flex')
    }, [props.status])

    return (<li className="todo-app__item" style={{display: display}}>
        <div className="todo-app__checkbox">
            <input type="checkbox" id={props.length} onChange={modifyComplete}/>
            <label htmlFor={props.length}/>
        </div>
        <h1 className="todo-app__item-detail">
            {complete===false?props.value:<del>{props.value}</del>}
        </h1>
        <img src="./img/x.png" className="todo-app__item-x" onClick={()=>deleteTodo()}/>
    </li>)
}

export default TodoItem;