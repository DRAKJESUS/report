from fastapi import APIRouter, Query, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database import get_db
import pandas as pd
import os
from datetime import datetime

router = APIRouter(prefix="/reportes", tags=["Reportes"])

async def generar_excel_desde_filas(rows, claveM, extra_nombre=""):
    registros = []
    for row in rows:
        nombre = row.nombre_completo or ""
        partes = nombre.split(' ')
        registros.append({
            "Matrícula": row.matricula,
            "Nombre": partes[0] if len(partes) > 0 else "",
            "Apellido Paterno": partes[1] if len(partes) > 1 else "",
            "Apellido Materno": partes[2] if len(partes) > 2 else "",
            "Asistencia": "Presente" if row.presente else "Ausente",
            "Fecha": row.fecha.strftime("%Y-%m-%d") if row.fecha else ""
        })

    df = pd.DataFrame(registros)
    filename = f"asistencia_{claveM}{extra_nombre}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    path = os.path.join("temp_excel", filename)
    os.makedirs("temp_excel", exist_ok=True)
    df.to_excel(path, index=False)
    return path, filename

@router.get("/excel_asistencias")
async def exportar_excel_asistencias(
    claveM: str = Query(...),
    numGrup: int = Query(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = '''
            SELECT 
                a.matricula,
                CONCAT(al.nombre, ' ', al.ape1, ' ', IFNULL(al.ape2, '')) AS nombre_completo,
                a.presente,
                a.fecha
            FROM ASISTENCIA a
            JOIN ALUMNO al ON a.matricula = al.matricula
            JOIN MATERIA m ON a.claveM = m.claveM
            JOIN GRUPO g ON a.numGrup = g.numGrup
            WHERE m.claveM = :claveM AND g.numGrup = :numGrup
            ORDER BY a.fecha DESC
        '''
        result = await db.execute(text(query), {'claveM': claveM, 'numGrup': numGrup})
        rows = result.fetchall()
        if not rows:
            raise HTTPException(status_code=404, detail="No se encontraron registros")

        path, filename = await generar_excel_desde_filas(rows, claveM, f"_grupo{numGrup}")
        return FileResponse(path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename=filename)

    except Exception as e:
        print("Error generando Excel:", e)
        raise HTTPException(status_code=500, detail=str(e))