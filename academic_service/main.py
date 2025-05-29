from fastapi import FastAPI, HTTPException

app = FastAPI(title="Academic Service")

# Mock de datos de estudiantes
students = {
    1: {"name": "Domenica Escobar", "programa": "Ingeniería de Sistemas"},
    2: {"name": "Alejandro Perez",  "programa": "Derecho"}
}

@app.get("/academico/{student_id}")
def get_student(student_id: int):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return {"id": student_id, **students[student_id]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
