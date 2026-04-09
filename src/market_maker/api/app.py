from fastapi import FastAPI
from market_maker.api.routes.health import router as health_router
from market_maker.api.routes.positions import router as positions_router
from market_maker.api.routes.pnl import router as pnl_router
from market_maker.api.routes.quotes import router as quotes_router
from market_maker.api.routes.controls import router as controls_router

app = FastAPI(title="market-maker-py")
app.include_router(health_router)
app.include_router(positions_router)
app.include_router(pnl_router)
app.include_router(quotes_router)
app.include_router(controls_router)
