from fastapi import FastAPI

from endpoint_observatory.simulator import router as sim_router

app = FastAPI()
app.include_router(sim_router)
