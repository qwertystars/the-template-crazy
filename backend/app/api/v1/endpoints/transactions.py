"""
Transaction management endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.transaction import Transaction, TransactionType, TransactionStatus
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.middleware.auth import get_current_active_user, require_admin


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new transaction.

    Args:
        transaction_data: Transaction creation data
        db: Database session
        current_user: Current authenticated user

    Returns:
        Created transaction
    """
    # Calculate total amount
    total_amount = transaction_data.amount * transaction_data.quantity

    if transaction_data.tax_amount:
        total_amount += transaction_data.tax_amount

    if transaction_data.discount_amount:
        total_amount -= transaction_data.discount_amount

    # Create transaction
    db_transaction = Transaction(
        **transaction_data.model_dump(),
        total_amount=total_amount,
        user_id=transaction_data.user_id or current_user.id,
    )

    db.add(db_transaction)
    await db.commit()
    await db.refresh(db_transaction)
    return db_transaction


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Get transaction by ID.

    Args:
        transaction_id: Transaction ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        Transaction details

    Raises:
        HTTPException: If transaction not found or not accessible
    """
    result = await db.execute(
        select(Transaction).where(Transaction.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    # Users can only see their own transactions unless admin
    if transaction.user_id != current_user.id and not current_user.is_superuser and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )

    return transaction


@router.get("/", response_model=List[TransactionResponse])
async def list_transactions(
    skip: int = 0,
    limit: int = 100,
    transaction_type: Optional[TransactionType] = None,
    status: Optional[TransactionStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    List transactions.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        transaction_type: Filter by transaction type
        status: Filter by status
        db: Database session
        current_user: Current authenticated user

    Returns:
        List of transactions
    """
    query = select(Transaction)

    # Non-admin users only see their own transactions
    if not current_user.is_superuser and current_user.role.value != "admin":
        query = query.where(Transaction.user_id == current_user.id)

    # Apply filters
    if transaction_type:
        query = query.where(Transaction.transaction_type == transaction_type)

    if status:
        query = query.where(Transaction.status == status)

    # Apply pagination
    query = query.offset(skip).limit(limit)

    result = await db.execute(query)
    transactions = result.scalars().all()
    return transactions


@router.put("/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: int,
    transaction_update: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Update transaction (admin only).

    Args:
        transaction_id: Transaction ID
        transaction_update: Transaction update data
        db: Database session
        current_user: Current authenticated admin user

    Returns:
        Updated transaction

    Raises:
        HTTPException: If transaction not found
    """
    result = await db.execute(
        select(Transaction).where(Transaction.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()

    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found",
        )

    # Update fields
    update_data = transaction_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transaction, field, value)

    await db.commit()
    await db.refresh(transaction)
    return transaction
