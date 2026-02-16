db = db.getSiblingDB("reservas_hotel")

// Limpeza para reexecução idempotente
db.clientes.deleteMany({})
db.quartos.deleteMany({})
db.reservas.deleteMany({})

// INSERTS
db.clientes.insertMany([
  {
    _id: ObjectId("65f100000000000000000001"),
    nome: "Mariana Souza",
    cpf: "123.456.789-00",
    telefone: "(89) 99999-1111",
    email: "mariana.souza@email.com",
    endereco: { rua: "Rua das Palmeiras", numero: 120, cidade: "Picos", uf: "PI" },
    data_cadastro: ISODate("2026-02-10T09:00:00Z")
  },
  {
    _id: ObjectId("65f100000000000000000002"),
    nome: "Carlos Henrique",
    cpf: "987.654.321-00",
    telefone: "(89) 99999-2222",
    email: "carlos.henrique@email.com",
    endereco: { rua: "Av. Central", numero: 45, cidade: "Picos", uf: "PI" },
    data_cadastro: ISODate("2026-02-10T09:30:00Z")
  },
  {
    _id: ObjectId("65f100000000000000000003"),
    nome: "Ana Paula Lima",
    cpf: "456.123.789-55",
    telefone: "(89) 99999-3333",
    email: "ana.paula@email.com",
    endereco: { rua: "Travessa São José", numero: 87, cidade: "Picos", uf: "PI" },
    data_cadastro: ISODate("2026-02-11T08:20:00Z")
  },
  {
    _id: ObjectId("65f100000000000000000004"),
    nome: "João Pedro Rocha",
    cpf: "321.654.987-77",
    telefone: "(89) 99999-4444",
    email: "joaopedro@email.com",
    endereco: { rua: "Rua Coelho Rodrigues", numero: 300, cidade: "Picos", uf: "PI" },
    data_cadastro: ISODate("2026-02-11T10:15:00Z")
  },
  {
    _id: ObjectId("65f100000000000000000005"),
    nome: "Fernanda Alves",
    cpf: "741.852.963-11",
    telefone: "(89) 99999-5555",
    email: "fernanda.alves@email.com",
    endereco: { rua: "Rua Projetada A", numero: 19, cidade: "Picos", uf: "PI" },
    data_cadastro: ISODate("2026-02-12T11:45:00Z")
  }
])

db.quartos.insertMany([
  { _id: ObjectId("65f200000000000000000001"), numero: "101", tipo: "Standard", capacidade: 2, diaria: 140.00, status: "disponivel", comodidades: ["Ar-condicionado", "Wi-Fi", "TV"] },
  { _id: ObjectId("65f200000000000000000002"), numero: "102", tipo: "Standard", capacidade: 3, diaria: 160.00, status: "disponivel", comodidades: ["Ventilador", "Wi-Fi", "TV"] },
  { _id: ObjectId("65f200000000000000000003"), numero: "201", tipo: "Luxo", capacidade: 2, diaria: 250.00, status: "ocupado", comodidades: ["Ar-condicionado", "Frigobar", "Wi-Fi", "TV Smart"] },
  { _id: ObjectId("65f200000000000000000004"), numero: "202", tipo: "Master", capacidade: 4, diaria: 320.00, status: "disponivel", comodidades: ["Ar-condicionado", "Frigobar", "Wi-Fi", "TV Smart", "Banheira"] },
  { _id: ObjectId("65f200000000000000000005"), numero: "301", tipo: "Econômico", capacidade: 2, diaria: 110.00, status: "manutencao", comodidades: ["Ventilador", "Wi-Fi"] }
])

db.reservas.insertMany([
  { _id: ObjectId("65f300000000000000000001"), cliente_id: ObjectId("65f100000000000000000001"), quarto_id: ObjectId("65f200000000000000000001"), data_checkin: ISODate("2026-02-20T14:00:00Z"), data_checkout: ISODate("2026-02-22T12:00:00Z"), qtd_hospedes: 2, valor_total: 280.00, status: "confirmada", forma_pagamento: "pix" },
  { _id: ObjectId("65f300000000000000000002"), cliente_id: ObjectId("65f100000000000000000002"), quarto_id: ObjectId("65f200000000000000000003"), data_checkin: ISODate("2026-02-18T14:00:00Z"), data_checkout: ISODate("2026-02-21T12:00:00Z"), qtd_hospedes: 2, valor_total: 750.00, status: "hospedado", forma_pagamento: "cartao_credito" },
  { _id: ObjectId("65f300000000000000000003"), cliente_id: ObjectId("65f100000000000000000003"), quarto_id: ObjectId("65f200000000000000000002"), data_checkin: ISODate("2026-02-25T14:00:00Z"), data_checkout: ISODate("2026-02-27T12:00:00Z"), qtd_hospedes: 3, valor_total: 320.00, status: "confirmada", forma_pagamento: "dinheiro" },
  { _id: ObjectId("65f300000000000000000004"), cliente_id: ObjectId("65f100000000000000000004"), quarto_id: ObjectId("65f200000000000000000004"), data_checkin: ISODate("2026-02-15T14:00:00Z"), data_checkout: ISODate("2026-02-16T12:00:00Z"), qtd_hospedes: 4, valor_total: 320.00, status: "finalizada", forma_pagamento: "pix" },
  { _id: ObjectId("65f300000000000000000005"), cliente_id: ObjectId("65f100000000000000000005"), quarto_id: ObjectId("65f200000000000000000005"), data_checkin: ISODate("2026-02-28T14:00:00Z"), data_checkout: ISODate("2026-03-01T12:00:00Z"), qtd_hospedes: 2, valor_total: 110.00, status: "pendente", forma_pagamento: "cartao_debito" }
])

// READ
const totalClientes = db.clientes.countDocuments({})
const quartosDisponiveis = db.quartos.countDocuments({ status: "disponivel" })
const reservasAcima300 = db.reservas.countDocuments({ valor_total: { $gt: 300 } })

// UPDATE
db.clientes.updateOne(
  { nome: "Mariana Souza" },
  { $set: { "endereco.bairro": "Centro" } }
)

db.quartos.updateOne(
  { numero: "301" },
  { $set: { status: "disponivel" } }
)

db.reservas.updateOne(
  { _id: ObjectId("65f300000000000000000005") },
  { $set: { status: "confirmada", forma_pagamento: "pix" } }
)

// DELETE
db.reservas.deleteOne({ _id: ObjectId("65f300000000000000000004") })
db.clientes.deleteOne({ cpf: "741.852.963-11" })

print("--- RESUMO EXECUÇÃO ---")
print("DB:", db.getName())
print("Clientes:", db.clientes.countDocuments({}))
print("Quartos:", db.quartos.countDocuments({}))
print("Reservas:", db.reservas.countDocuments({}))
print("Quartos disponíveis:", db.quartos.countDocuments({ status: "disponivel" }))
print("Reservas confirmadas:", db.reservas.countDocuments({ status: "confirmada" }))
print("Leitura prévia - totalClientes:", totalClientes)
print("Leitura prévia - quartosDisponiveis:", quartosDisponiveis)
print("Leitura prévia - reservasAcima300:", reservasAcima300)
