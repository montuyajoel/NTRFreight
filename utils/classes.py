from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any, Tuple

@dataclass(frozen=True)
class Region:
    id: int
    matching_strategy: str
    client: str
    carrier: Optional[str] = None
    country: Optional[str] = None
    zipcode: Optional[str] = None
    city: Optional[str] = None
    airport: Optional[str] = None
    seaport: Optional[str] = None
    identifier_string: Optional[str] = None

    def key(self) -> Tuple:
        return (
            self.country or "",
            self.zipcode or "",
            self.city or "",
            self.airport or "",
            self.seaport or "",
            self.identifier_string or "",
        )
    
@dataclass
class TariffRow:
    id: int
    start_date: Optional[str]
    end_date: Optional[str]
    client: str
    carrier: str
    route: Any  
    currency: Optional[str]
    service_type: Optional[str]
    ldm_conversion: Optional[float] = None
    cbm_conversion: Optional[float] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    # dynamic band columns appended later