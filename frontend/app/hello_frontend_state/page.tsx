'use client'
import React, { useEffect,useState } from 'react'
export default function Page() {
    const [data, seData]=useState({name:'初期値'})

    useEffect(() =>{
        const change = {name:'変更'}
        seData(change)
    }, [])

    return <div>hello {data.name}!</div>
}