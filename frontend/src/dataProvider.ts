const API_URL = "http://localhost:8000";

const idFields = {
  staff: "staff_no",
  branch: "branch_no",
  client: "client_no",
};

const mapId = (resource) => (record) => ({
  ...record,
  id: record[idFields[resource]],
});

export const dataProvider = {
  getList: async (resource, params) => {
    const { page, perPage } = params.pagination;
    const { field, order } = params.sort;
    const { filter } = params;
    const query = {
      _page: page,
      _limit: perPage,
      _sort: field,
      _order: order,
      filter: JSON.stringify(filter?.filters),
    };
    const searchParams = new URLSearchParams(query).toString();
    const response = await fetch(`${API_URL}/${resource}?${searchParams}`, {
      mode: "cors",
      headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();
    const total = response.headers.get("X-Total-Count");
    return { data: data.map(mapId(resource)), total: total };
  },

  getOne: async (resource, params) => {
    const response = await fetch(`${API_URL}/${resource}/${params.id}`, {
      mode: "cors",
      headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();
    return { data: mapId(resource)(data) };
  },

  getMany: async (resource, params) => {
    const response = await fetch(`${API_URL}/${resource}`, {
      mode: "cors",
      headers: { "Content-Type": "application/json" },
    });
    const data = await response.json();
    return {
      data: data
        .map(mapId(resource))
        .filter((elt) => params.ids.includes(elt.id)),
    };
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
