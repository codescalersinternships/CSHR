import type { UserInterface } from "../../../types";
import http from "../http-common";
class UsersDataService {
    errorMessage: string = "Error in Users Data Service: ";
    public async getAll() {
        try {
            const { data, status, statusText } = (await http.get(`/users/`));
            if (status === 404) {
                throw new Error("Users not found");
            }
            else if (status !== 200) {
                throw new Error("Error in getting users with status " + status + " wtih status text : " + statusText);
            }
            return data.results;

        } catch (err) {
            console.error(this.errorMessage + err);
            throw new Error(err);

        }
    }
    public async getById(id: number): Promise<UserInterface> {
        try {
            const { data, status, statusText } = (await http.get(`/users/${id}/`));
            if (status === 404) {
                throw new Error("User not found");
            }
            else if (status !== 200) {
                throw new Error("Error in getting users with status " + status + " wtih status text : " + statusText);
            }
            return data.results;
        } catch (err) {
            console.error(this.errorMessage + err);
            throw new Error(err);
        }
    }
}

const usersDataService = new UsersDataService();
export default usersDataService;