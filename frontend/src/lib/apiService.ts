export const apiService = {

    getRefreshToken: async function (): Promise<any> {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/usuarios/refresh/`,{
                    method: "POST",
                    credentials: "include",
                }
            );

            // ❌ Refresh falló (cookie inválida / expirada)
            if (!response.ok) {
                //return false;
                const errorData = await response.json()
                return errorData
            }

            // ✅ Refresh OK → cookies renovadas
            //return true;
            const data = await response.json()
            return data

        } catch (error) {
            console.error("Error en refresh token:", error);
            return false;
        }
    },

    get: async function (url: string): Promise<any> {
        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${url}`,
                {
                    method: "GET",
                    credentials: "include",
                }
            );
            console.log("Response es", response)
            // ✅ SOLO refrescar si es 401
            if (response.status === 401) { //if (!response.ok) {
                console.log("STATUS ES ===", response.status)
                const refreshed = await apiService.getRefreshToken() || null;
                console.log("refreshed; ", refreshed)
                if (refreshed?.message) {
                    console.log("ENTRA EN REFRESHED ENTRA EN REFRESHED ENTRA EN REFRESHED ENTRA EN REFRESHED")
                    // 🔁 Reintentamos UNA sola vez
                    return await apiService.get(url);
                }

                // ❌ Refresh falló → logout real
                if (!refreshed) {
                    // ❌ No hagas redirect desde aquí
                    // window.location.href = "/";
                    throw new Error("Usuario no autenticado");
                }
            }

            // ❌ Otros errores reales
            if (!response.ok) {
                const errorData = await response.json();
                throw errorData;
            }

            // ✅ OK
            return await response.json();

        } catch (error) {
            console.error("Error en GET:", error);
            throw error; // importante para que el caller lo maneje
        }
    }
    

}