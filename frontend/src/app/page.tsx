"use client";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { apiService } from "@/lib/apiService";
import { useEffect, useState } from "react";


export default function Home() {
  const [email, setEmail] = useState("")
  const [username, setUsername] = useState("")
  const [password, setPasword] = useState("")

  const [session, setSesion] = useState(null)

  const onSubmit = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/usuarios/registro/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username,
          email,
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json()
        console.error(errorData)
        return errorData
      }

      const data = await response.json();
      console.log("Usuario creado:", data);
      //

    } catch (error) {
      console.error("Error:", error);
    }
  };

  const onLogin = async() => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/usuarios/login/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({
          email,
          password,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json()
        console.error(errorData)
        return errorData
      }

      const data = await response.json();
      setSesion(data.username)
      console.log("Usuario logado:", data);
      //

    } catch (error) {
      console.error("Error:", error);
    }
  }

  const onLogout = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/api/usuarios/logout/", {
        method: "POST",
        credentials: "include",
      });

      if (!response.ok) {
        const errorData = await response.json()
        console.error(errorData)
        return errorData
      }

      const data = await response.json();
      console.log("Usuario DESLOGADO:", data);
      setSesion(null)
      //

    } catch (error) {
      console.error("Error:", error);
    }
    /*
    } finally {
      // 🔥 CORTE DEFINITIVO DE SESIÓN
      setSesion(null)
      // opcional: router.push("/login")
    }
      */
  }

  useEffect(() => {
   
      const fetchSession = async () => {
        try {
          const data = await apiService.get('/usuarios/me/')
          setSesion(data.username)
        } catch (error) {
          console.error('Error cargando usuario', error)
          // Aquí puedes redirigir a login de manera controlada
          // router.push("/login")

        }
      }
      fetchSession()
    
  }, [session])

  if (session) {
    return (
      <div className="p-4 flex flex-col gap-y-4">
          <p>Logado como: </p>{session}
          <Button className="cursor-pointer" onClick={onLogout}>
            Logout
          </Button>
      </div>
    )
  } 

  return (
    <div className="p-4 flex flex-col gap-y-4">
      <Input 
        placeholder="email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)}
      />
      <Input 
        placeholder="password" 
        type="password" 
        value={password} 
        onChange={(e) => setPasword(e.target.value)}
      />
      <Button 
        type="button"
        className = "cursor-pointer" 
        onClick={onLogin}
      >
        Login usuario
      </Button>
    


    
      <Input 
        placeholder="name" 
        value={username} 
        onChange={(e) => setUsername(e.target.value)}
      />
      <Input 
        placeholder="email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)}
      />
      <Input 
        placeholder="password" 
        type="password" 
        value={password} 
        onChange={(e) => setPasword(e.target.value)}
      />
      <Button 
        type="button"
        className = "cursor-pointer" 
        onClick={onSubmit}
      >
        Crear usuario
      </Button>
    </div>
  );
}
