from fastapi import APIRouter, HTTPException, status

from schemas.ticket import TicketResponse

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
