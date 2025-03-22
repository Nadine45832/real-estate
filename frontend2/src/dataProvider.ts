const API_URL = "http://localhost:8000";

const idFields = {
  staff: "staff_no",
  branches: "branch_id",
  clients: "client_id",
};

const mapId = (resource) => (record) => ({
  ...record,
  id: record[idFields[resource]],
});

export const dataProvider = {
  getList: async (resource, params) => {
    const response = await fetch(`${API_URL}/${resource}`, {
      mode: "cors",
      headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();
    return { data: data.map(mapId(resource)), total: data.length };
  },

  getOne: async (resource, params) => {
    const response = await fetch(`${API_URL}/${resource}/${params.id}`, {
      mode: "cors",
      headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();
    return { data: mapId(resource)(data) };
  },

  create: async (resource, params) => {
    const response = await fetch(`${API_URL}/${resource}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params.data),
      mode: "cors",
    });
    const data = await response.json();
    return { data: mapId(resource)(data) };
  },

  update: async (resource, params) => {
    const response = await fetch(`${API_URL}/${resource}/${params.id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(params.data),
      mode: "cors",
    });
    const data = await response.json();
    return { data: mapId(resource)(data) };
  },

  delete: async (resource, params) => {
    await fetch(`${API_URL}/${resource}/${params.id}`, {
      method: "DELETE",
      mode: "cors",
    });
    return { data: { id: params.id } };
  },
};
