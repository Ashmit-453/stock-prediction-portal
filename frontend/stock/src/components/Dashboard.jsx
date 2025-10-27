import React from 'react'
import {useEffect, useState} from 'react'
import axiosInstance from './../axiosInstance'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faSpinner } from '@fortawesome/free-solid-svg-icons'
const Dashboard = () => {
   useEffect(()=>{
        const fetchProtectedData = async () =>{
            try{
                const response = await axiosInstance.get('/protected-view/');
            }catch(error){
                console.error('Error fetching data:', error)
            }
        }
        fetchProtectedData();
    }, [])
  return (
    <div>Dashboard</div>
  )
}

export default Dashboard