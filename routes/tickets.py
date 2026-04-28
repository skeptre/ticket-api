from datetime import datetime

from fastapi import APIRouter, HTTPException, status

from schemas.ticket import (
    TicketCreate,
    TicketResponse,
    TicketStatus,
    TicketUpdate,
)

router = APIRouter(prefix="/tickets", tags=["tickets"])

# In-memory ticket storage for demo purposes
tickets_db: list[TicketResponse] = []


@router.get("/", response_model=list[TicketResponse])
def get_tickets() -> list[TicketResponse]:
    """Get all tickets."""
    return tickets_db


@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: int) -> TicketResponse:
    """Get a single ticket by ID."""
    for ticket in tickets_db:
        if ticket.id == ticket_id:
            return ticket

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Ticket with id {ticket_id} not found",
    )


@router.post("/", response_model=TicketResponse, status_code=status.HTTP_201_CREATED)
def create_ticket(ticket: TicketCreate) -> TicketResponse:
    """Create a new ticket."""
    now = datetime.utcnow()
    new_ticket = TicketResponse(
        id=len(tickets_db) + 1,
        title=ticket.title,
        description=ticket.description,
        status=TicketStatus.OPEN,
        priority=ticket.priority,
        owner_id=1,
        created_at=now,
        updated_at=now,
    )
    tickets_db.append(new_ticket)
    return new_ticket


@router.patch("/{ticket_id}", response_model=TicketResponse)
def patch_ticket(ticket_id: int, updated_ticket: TicketUpdate) -> TicketResponse:
    """Update a ticket by ID."""
    for index, ticket in enumerate(tickets_db):
        if ticket.id == ticket_id:
            update_data = updated_ticket.model_dump(exclude_unset=True)

            updated_ticket_data = ticket.model_dump()
            updated_ticket_data.update(update_data)
            updated_ticket_data["updated_at"] = datetime.utcnow()

            tickets_db[index] = TicketResponse(**updated_ticket_data)
            return tickets_db[index]

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Ticket with id {ticket_id} not found",
    )


@router.delete("/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(ticket_id: int) -> None:
    """Delete a ticket by ID."""
    for index, ticket in enumerate(tickets_db):
        if ticket.id == ticket_id:
            del tickets_db[index]
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Ticket with id {ticket_id} not found",
    )