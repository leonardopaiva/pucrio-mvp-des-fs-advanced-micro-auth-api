from .auth import LoginSchema, RegistrationSchema, ConfirmSignUpSchema, ResetPasswordSchema, ProtectedInputSchema, TokenResponseSchema, RefreshSchema, ErrorSchema
from schemas.comentario import ComentarioSchema
from schemas.user import UserSchema, UserBuscaSchema, UserViewSchema, \
                            ListagemUsersSchema, UserDelSchema, apresenta_users, \
                            apresenta_user, apresenta_users
from schemas.produto import ProdutoSchema, ProdutoBuscaSchema, ProdutoViewSchema, \
                            ListagemProdutosSchema, ProdutoDelSchema, apresenta_produtos, \
                            apresenta_produto, apresenta_produtos
from schemas.event import EventSchema, EventBuscaSchema, EventViewSchema, \
                            ListagemEventsSchema, EventDelSchema, apresenta_events, \
                            apresenta_event, apresenta_events
from schemas.doctor import DoctorSchema, DoctorBuscaSchema, DoctorViewSchema, \
                            ListagemDoctorsSchema, DoctorDelSchema, apresenta_doctors, \
                            apresenta_doctor, apresenta_doctors
from schemas.specialty import SpecialtySchema, SpecialtyBuscaSchema, SpecialtyViewSchema, \
                            ListagemSpecialtiesSchema, SpecialtyDelSchema, apresenta_specialties, \
                            apresenta_specialty, apresenta_specialties
from schemas.location import LocationSchema, LocationBuscaSchema, LocationViewSchema, \
                            ListagemLocationsSchema, LocationDelSchema, apresenta_locations, \
                            apresenta_location, apresenta_locations
from schemas.error import ErrorSchema
