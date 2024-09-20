'use client'
import React,{useState, useEffecgt, useEffect} from 'react';
import productsData from "./sample/dummy_products.json";
import Link from "next/link";
import SelectInput from '@mui/material/Select/SelectInput';

type ProductData={
    id: number;
    name: string;
    price: string;
    description: string;
};

type InputData={
    id: string;
    name: string;
    price: string;
    description: string;
}

export default function Page(){
    // 読み込みデータ保持,
    // data⇒状態の値を保持、
    // setData⇒これを呼び出すことで状態を更新して再レンダリングする
    // useState⇒Reactにフック、状態を管理できる、引数は初期値
    // <>はTSの型指定、ProductData型の配列
    const [data, setData]= useState<Array<ProductData>>([]);
    // 登録データの保持
    const [input, setInput]=useState<InputData>({
        id: "",
        name: "",
        price: "",
        description: "",
    })
    // 登録データの更新
    const handleInput=(event: React.ChangeEvent<HTMLInputElement>)=>{
        const {value,name}=event.target;
        setInput({ ...input,[name]:value});
    }
    // 副作用を管理するためのフック、
    useEffect(()=>{
        setData(productsData);
    },[])
    
    // 新規登録処理、新規登録行の表示状態を保持
    const [shownNewRow, setShowNewRow]=useState(false);
    const handleShowNewRow=(event: React.MouseEvent<HTMLElement>)=>{
        event.preventDefault();
        setShowNewRow(true)
    };
    const handleAddCancel=(event: React.MouseEvent<HTMLElement>)=>{
        event.preventDefault();
        setShowNewRow(false)
    };
    const handleAdd=(event: React.MouseEvent<HTMLElement>)=>{
        event.preventDefault();
        // バックエンドを使用した登録処理を呼ぶ
        setShowNewRow(false)
    };

    // 更新・削除処理、更新・削除行の表示状態を保持
    const [editingRow, setEditingRow]=useState(0);
    const handleEditRow: any=(id: number)=>{
        setShowNewRow(false);
        setEditingRow(id);
        const selectedProduct: ProductData=data.find((v)=>v.id === id) as ProductData;
        setInput({
            id: id.toLocaleString(),
            name: selectedProduct.name,
            price: selectedProduct.price.toString(),
            description: selectedProduct.description,
        })
    };
    const handleEditCancel: any=(id: number)=>{
        setEditingRow(0)
    };
    const handleEdit: any=(id: number)=>{
        setEditingRow(0)
    };
    const handleDelete: any=(id: number)=>{
        setEditingRow(0)
    }
    
    return (
        <>
        <h2>商品一覧</h2>
        <button onClick={ handleShowNewRow }>商品を追加する</button>
        <table>
            <thead>
                <tr>
                    <th>商品ID</th>
                    <th>商品名</th>
                    <th>単価</th>
                    <th>説明</th>
                    <th></th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {shownNewRow ? (
                    <tr>
                        <td></td>
                        <td><input type="text" name="name" onChange={handleInput}/></td>
                        <td><input type="number" name="price" onChange={handleInput}/></td>
                        <td><input type="text" name="description" onChange={handleInput}/></td>
                        <td></td>
                        <td><button onClick={(event)=>handleAddCancel(event)}>キャンセル</button><button onClick={(event)=>handleAdd(event)}>登録する</button></td>
                    </tr>
                ) : ""}
                {data.map((data: any)=>(
                    editingRow === data.id ? (
                        <tr key={data.id}>
                            <td>{data.id}</td>
                            <td><input type="text" value={input.name} name="name" onChange={handleInput}/></td>
                            <td><input type="number" value={input.price} name="price" onChange={handleInput}/></td>
                            <td><input type="text" value={input.description} name="description" onChange={handleInput}/></td>
                            <td></td>
                            <td><button onClick={()=>handleEdit(data.id)}>キャンセル</button>
                            <button onClick={()=>handleEdit(data.id)}>更新する</button>
                            <button onClick={()=>handleDelete(data.id)}>削除する</button></td>
                        </tr>
                    ) : (
                    <tr key={data.id}>
                        <td>{data.id}</td>
                        <td>{data.name}</td>
                        <td>{data.price}</td>
                        <td>{data.description}</td>
                        <td><Link href={'/inventory/products/${data.id}'}>在庫処理</Link></td>
                        <td><button onClick={()=>handleEditRow(data.id)}>更新・削除</button></td>
                    </tr>
                )
                ))}
            </tbody>
        </table>
        </>
    )
}