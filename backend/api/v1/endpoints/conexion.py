import email
from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response

router = APIRouter()


# GET current user
@router.get('/')
def is_online():
    return Response(status_code=status.HTTP_200_OK)
